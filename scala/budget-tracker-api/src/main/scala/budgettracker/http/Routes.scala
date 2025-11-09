package budgettracker.http

import cats.effect.*
import cats.implicits.*
import org.http4s.*
import org.http4s.dsl.Http4sDsl
import org.http4s.circe.*
import org.http4s.circe.CirceEntityDecoder.*
import org.http4s.circe.CirceEntityEncoder.*
import io.circe.syntax.*
import io.circe.generic.auto.*
import budgettracker.domain.*
import budgettracker.service.*
import java.time.LocalDateTime
import java.util.UUID

object AuthMiddleware:
  def extractUserId[F[_]: Sync](req: Request[F]): F[Either[String, UserId]] =
    Sync[F].pure {
      req.headers.get(ci"X-User-Id").flatMap { h =>
        try Some(UserId(UUID.fromString(h.head.value)))
        catch case _: IllegalArgumentException => None
      }.toRight("Missing or invalid X-User-Id header")
    }

class AuthRoutes[F[_]: Sync](authService: AuthService[F]) extends Http4sDsl[F]:
  val routes: HttpRoutes[F] = HttpRoutes.of[F] {
    case req @ POST -> Root / "auth" / "register" =>
      for {
        createReq <- req.as[CreateUserRequest]
        result <- authService.register(createReq)
        response <- result match
          case Right(user) => Created(Map("userId" -> user.id.value.toString, "username" -> user.username).asJson)
          case Left(ServiceError.UserAlreadyExists(u)) => Conflict(Map("error" -> s"User $u exists").asJson)
          case Left(ServiceError.ValidationErrors(e)) => BadRequest(Map("error" -> e.toList.toString).asJson)
          case Left(other) => InternalServerError(Map("error" -> other.toString).asJson)
      } yield response

    case req @ POST -> Root / "auth" / "login" =>
      for {
        loginReq <- req.as[LoginRequest]
        result <- authService.login(loginReq)
        response <- result match
          case Right(auth) => Ok(auth.asJson)
          case Left(ServiceError.InvalidCredentials) => Unauthorized(Map("error" -> "Invalid credentials").asJson)
          case Left(ServiceError.UserNotFound(u)) => NotFound(Map("error" -> s"User $u not found").asJson)
          case Left(other) => InternalServerError(Map("error" -> other.toString).asJson)
      } yield response
  }

class TransactionRoutes[F[_]: Sync](txService: TransactionService[F]) extends Http4sDsl[F]:
  object FromParam extends OptionalQueryParamDecoderMatcher[String]("from")
  object ToParam extends OptionalQueryParamDecoderMatcher[String]("to")

  val routes: HttpRoutes[F] = HttpRoutes.of[F] {
    case req @ POST -> Root / "transactions" =>
      (for {
        userId <- Sync[F].fromEither(AuthMiddleware.extractUserId(req).flatMap(Sync[F].pure).flatten.leftMap(new RuntimeException(_)))
        createReq <- req.as[CreateTransactionRequest]
        tx <- txService.create(createReq, userId)
        response <- Created(tx.asJson)
      } yield response).handleErrorWith(err => Unauthorized(Map("error" -> err.getMessage).asJson))

    case req @ GET -> Root / "transactions" :? FromParam(from) +& ToParam(to) =>
      (for {
        userId <- Sync[F].fromEither(AuthMiddleware.extractUserId(req).flatMap(Sync[F].pure).flatten.leftMap(new RuntimeException(_)))
        txs <- (from, to) match
          case (Some(f), Some(t)) => txService.getByDateRange(userId, LocalDateTime.parse(f), LocalDateTime.parse(t))
          case _ => txService.getAll(userId)
        response <- Ok(txs.asJson)
      } yield response).handleErrorWith(err => BadRequest(Map("error" -> err.getMessage).asJson))

    case req @ DELETE -> Root / "transactions" / UUIDVar(id) =>
      (for {
        userId <- Sync[F].fromEither(AuthMiddleware.extractUserId(req).flatMap(Sync[F].pure).flatten.leftMap(new RuntimeException(_)))
        result <- txService.delete(TransactionId(id), userId)
        response <- result match
          case Right(_) => NoContent()
          case Left(ServiceError.TransactionNotFound(_)) => NotFound(Map("error" -> "Not found").asJson)
          case Left(other) => InternalServerError(Map("error" -> other.toString).asJson)
      } yield response).handleErrorWith(err => Unauthorized(Map("error" -> err.getMessage).asJson))

    case req @ GET -> Root / "reports" / "budget" :? FromParam(from) +& ToParam(to) =>
      (for {
        userId <- Sync[F].fromEither(AuthMiddleware.extractUserId(req).flatMap(Sync[F].pure).flatten.leftMap(new RuntimeException(_)))
        report <- (from, to) match
          case (Some(f), Some(t)) => txService.getReportByDateRange(userId, LocalDateTime.parse(f), LocalDateTime.parse(t))
          case _ => txService.getReport(userId)
        response <- Ok(report.asJson)
      } yield response).handleErrorWith(err => BadRequest(Map("error" -> err.getMessage).asJson))
  }

object Routes:
  def make[F[_]: Sync](authService: AuthService[F], txService: TransactionService[F]): HttpRoutes[F] =
    new AuthRoutes[F](authService).routes <+> new TransactionRoutes[F](txService).routes
