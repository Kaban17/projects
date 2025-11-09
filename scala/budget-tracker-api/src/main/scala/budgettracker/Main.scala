package budgettracker

import cats.effect.*
import cats.implicits.*
import com.comcast.ip4s.*
import doobie.*
import doobie.hikari.HikariTransactor
import org.http4s.ember.server.EmberServerBuilder
import org.http4s.server.Server
import org.typelevel.log4cats.Logger
import org.typelevel.log4cats.slf4j.Slf4jLogger
import budgettracker.repository.*
import budgettracker.service.*
import budgettracker.http.Routes

object Main extends IOApp:
  given Logger[IO] = Slf4jLogger.getLogger[IO]

  case class DatabaseConfig(
    driver: String = "org.postgresql.Driver",
    url: String = "jdbc:postgresql://localhost:5432/budget_tracker",
    user: String = "postgres",
    password: String = "postgres"
  )

  def makeTransactor(config: DatabaseConfig): Resource[IO, HikariTransactor[IO]] =
    for {
      ce <- ExecutionContexts.fixedThreadPool[IO](32)
      xa <- HikariTransactor.newHikariTransactor[IO](config.driver, config.url, config.user, config.password, ce)
    } yield xa

  def initializeDatabase(xa: Transactor[IO]): IO[Unit] =
    val createUsers = sql"""CREATE TABLE IF NOT EXISTS users (
      id UUID PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, email VARCHAR(255) NOT NULL,
      password_hash VARCHAR(255) NOT NULL, created_at TIMESTAMP NOT NULL)""".update.run

    val createTxs = sql"""CREATE TABLE IF NOT EXISTS transactions (
      id UUID PRIMARY KEY, user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      amount DECIMAL(15, 2) NOT NULL, transaction_type VARCHAR(50) NOT NULL, category VARCHAR(50) NOT NULL,
      description TEXT, date TIMESTAMP NOT NULL, created_at TIMESTAMP NOT NULL)""".update.run

    val createIdx = sql"""CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
      CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date)""".update.run

    (createUsers *> createTxs *> createIdx).transact(xa).void
      .handleErrorWith(err => Logger[IO].error(err)("DB init failed") *> IO.raiseError(err))

  def makeServer(routes: org.http4s.HttpRoutes[IO]): Resource[IO, Server] =
    EmberServerBuilder.default[IO].withHost(ipv4"0.0.0.0").withPort(port"8080")
      .withHttpApp(routes.orNotFound).build

  def run(args: List[String]): IO[ExitCode] =
    val config = DatabaseConfig()
    val resources = for {
      xa <- makeTransactor(config)
      _ <- Resource.eval(initializeDatabase(xa))
      userRepo = UserRepository.make[IO](xa)
      txRepo = TransactionRepository.make[IO](xa)
      authService = AuthService.make[IO](userRepo)
      txService = TransactionService.make[IO](txRepo)
      routes = Routes.make[IO](authService, txService)
      server <- makeServer(routes)
    } yield server

    resources.use(server => Logger[IO].info(s"Server at ${server.address}") *> IO.never.as(ExitCode.Success))
