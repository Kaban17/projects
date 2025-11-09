package budgettracker.domain

import io.circe.{Decoder, Encoder}
import io.circe.generic.semiauto.*
import java.time.LocalDateTime
import java.util.UUID

opaque type UserId = UUID
object UserId:
  def apply(uuid: UUID): UserId = uuid
  def random: UserId = UUID.randomUUID()
  extension (id: UserId) def value: UUID = id

opaque type TransactionId = UUID
object TransactionId:
  def apply(uuid: UUID): TransactionId = uuid
  def random: TransactionId = UUID.randomUUID()
  extension (id: TransactionId) def value: UUID = id

enum Category:
  case Food, Transport, Entertainment, Utilities, Salary, Other

object Category:
  given Encoder[Category] = Encoder.encodeString.contramap(_.toString)
  given Decoder[Category] = Decoder.decodeString.emap { str =>
    try Right(Category.valueOf(str))
    catch case _: IllegalArgumentException => Left(s"Invalid category: $str")
  }

enum TransactionType:
  case Income, Expense

object TransactionType:
  given Encoder[TransactionType] = Encoder.encodeString.contramap(_.toString)
  given Decoder[TransactionType] = Decoder.decodeString.emap { str =>
    try Right(TransactionType.valueOf(str))
    catch case _: IllegalArgumentException => Left(s"Invalid type: $str")
  }

case class User(
  id: UserId,
  username: String,
  email: String,
  passwordHash: String,
  createdAt: LocalDateTime
)

case class Transaction(
  id: TransactionId,
  userId: UserId,
  amount: BigDecimal,
  transactionType: TransactionType,
  category: Category,
  description: Option[String],
  date: LocalDateTime,
  createdAt: LocalDateTime
)

object Transaction:
  given Encoder[Transaction] = deriveEncoder
  given Decoder[Transaction] = deriveDecoder

case class CreateUserRequest(username: String, email: String, password: String)
object CreateUserRequest:
  given Decoder[CreateUserRequest] = deriveDecoder

case class LoginRequest(username: String, password: String)
object LoginRequest:
  given Decoder[LoginRequest] = deriveDecoder

case class CreateTransactionRequest(
  amount: BigDecimal,
  transactionType: TransactionType,
  category: Category,
  description: Option[String],
  date: Option[LocalDateTime]
)
object CreateTransactionRequest:
  given Decoder[CreateTransactionRequest] = deriveDecoder

case class AuthResponse(token: String, userId: String)
object AuthResponse:
  given Encoder[AuthResponse] = deriveEncoder

case class CategoryReport(
  category: Category,
  totalIncome: BigDecimal,
  totalExpense: BigDecimal,
  balance: BigDecimal
)
object CategoryReport:
  given Encoder[CategoryReport] = deriveEncoder

case class BudgetReport(
  totalIncome: BigDecimal,
  totalExpense: BigDecimal,
  balance: BigDecimal,
  byCategory: List[CategoryReport]
)
object BudgetReport:
  given Encoder[BudgetReport] = deriveEncoder
