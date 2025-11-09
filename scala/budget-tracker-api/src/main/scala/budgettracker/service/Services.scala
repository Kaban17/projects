package budgettracker.service

import cats.*
import cats.effect.*
import cats.implicits.*
import cats.data.{NonEmptyList, ValidatedNel}
import cats.data.Validated.*
import budgettracker.domain.*
import budgettracker.repository.*
import com.github.t3hnar.bcrypt.*
import java.time.LocalDateTime
import java.util.UUID

enum ValidationError:
  case EmptyUsername, UsernameTooShort, InvalidEmail, PasswordTooShort, InvalidAmount

enum ServiceError:
  case UserAlreadyExists(username: String)
  case UserNotFound(username: String)
  case InvalidCredentials
  case TransactionNotFound(id: TransactionId)
  case Unauthorized
  case ValidationErrors(errors: NonEmptyList[ValidationError])

object Validation:
  def validateUsername(username: String): ValidatedNel[ValidationError, String] =
    if username.isEmpty then ValidationError.EmptyUsername.invalidNel
    else if username.length < 3 then ValidationError.UsernameTooShort.invalidNel
    else username.validNel

  def validateEmail(email: String): ValidatedNel[ValidationError, String] =
    val emailRegex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$".r
    if emailRegex.matches(email) then email.validNel else ValidationError.InvalidEmail.invalidNel

  def validatePassword(password: String): ValidatedNel[ValidationError, String] =
    if password.length < 6 then ValidationError.PasswordTooShort.invalidNel else password.validNel

  def validateCreateUser(req: CreateUserRequest): ValidatedNel[ValidationError, CreateUserRequest] =
    (validateUsername(req.username), validateEmail(req.email), validatePassword(req.password))
      .mapN((_, _, _) => req)

trait AuthService[F[_]]:
  def register(req: CreateUserRequest): F[Either[ServiceError, User]]
  def login(req: LoginRequest): F[Either[ServiceError, AuthResponse]]

object AuthService:
  def make[F[_]: Sync](userRepo: UserRepository[F]): AuthService[F] = new AuthService[F]:
    def register(req: CreateUserRequest): F[Either[ServiceError, User]] =
      Validation.validateCreateUser(req) match
        case Invalid(errors) => Sync[F].pure(Left(ServiceError.ValidationErrors(errors)))
        case Valid(_) =>
          userRepo.findByUsername(req.username).flatMap {
            case Some(_) => Sync[F].pure(Left(ServiceError.UserAlreadyExists(req.username)))
            case None =>
              val user = User(UserId.random, req.username, req.email, req.password.bcryptBounded(10), LocalDateTime.now())
              userRepo.create(user).map(Right(_))
          }

    def login(req: LoginRequest): F[Either[ServiceError, AuthResponse]] =
      userRepo.findByUsername(req.username).map {
        case None => Left(ServiceError.UserNotFound(req.username))
        case Some(user) =>
          if req.password.isBcryptedBounded(user.passwordHash)
          then Right(AuthResponse(UUID.randomUUID().toString, user.id.value.toString))
          else Left(ServiceError.InvalidCredentials)
      }

trait TransactionService[F[_]]:
  def create(req: CreateTransactionRequest, userId: UserId): F[Transaction]
  def getAll(userId: UserId): F[List[Transaction]]
  def getByDateRange(userId: UserId, from: LocalDateTime, to: LocalDateTime): F[List[Transaction]]
  def delete(id: TransactionId, userId: UserId): F[Either[ServiceError, Unit]]
  def getReport(userId: UserId): F[BudgetReport]
  def getReportByDateRange(userId: UserId, from: LocalDateTime, to: LocalDateTime): F[BudgetReport]

object TransactionService:
  def make[F[_]: Sync](repo: TransactionRepository[F]): TransactionService[F] = new TransactionService[F]:
    def create(req: CreateTransactionRequest, userId: UserId): F[Transaction] =
      val tx = Transaction(TransactionId.random, userId, req.amount, req.transactionType, req.category,
                          req.description, req.date.getOrElse(LocalDateTime.now()), LocalDateTime.now())
      repo.create(tx)

    def getAll(userId: UserId): F[List[Transaction]] = repo.findByUserId(userId)

    def getByDateRange(userId: UserId, from: LocalDateTime, to: LocalDateTime): F[List[Transaction]] =
      repo.findByUserIdAndDateRange(userId, from, to)

    def delete(id: TransactionId, userId: UserId): F[Either[ServiceError, Unit]] =
      repo.delete(id, userId).map(deleted => if deleted then Right(()) else Left(ServiceError.TransactionNotFound(id)))

    def getReport(userId: UserId): F[BudgetReport] = repo.findByUserId(userId).map(calculateReport)

    def getReportByDateRange(userId: UserId, from: LocalDateTime, to: LocalDateTime): F[BudgetReport] =
      repo.findByUserIdAndDateRange(userId, from, to).map(calculateReport)

    private def calculateReport(txs: List[Transaction]): BudgetReport =
      val byCategory = txs.groupBy(_.category).map { case (cat, ctxs) =>
        val income = ctxs.filter(_.transactionType == TransactionType.Income).map(_.amount).sum
        val expense = ctxs.filter(_.transactionType == TransactionType.Expense).map(_.amount).sum
        CategoryReport(cat, income, expense, income - expense)
      }.toList
      val totalIncome = txs.filter(_.transactionType == TransactionType.Income).map(_.amount).sum
      val totalExpense = txs.filter(_.transactionType == TransactionType.Expense).map(_.amount).sum
      BudgetReport(totalIncome, totalExpense, totalIncome - totalExpense, byCategory)
