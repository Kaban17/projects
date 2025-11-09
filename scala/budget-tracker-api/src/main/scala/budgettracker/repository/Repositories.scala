package budgettracker.repository

import cats.effect.*
import cats.implicits.*
import doobie.*
import doobie.implicits.*
import doobie.postgres.implicits.*
import budgettracker.domain.*
import java.time.LocalDateTime
import java.util.UUID

given Meta[UserId] = Meta[UUID].imap(UserId.apply)(_.value)
given Meta[TransactionId] = Meta[UUID].imap(TransactionId.apply)(_.value)
given Meta[Category] = Meta[String].imap(Category.valueOf)(_.toString)
given Meta[TransactionType] = Meta[String].imap(TransactionType.valueOf)(_.toString)

trait UserRepository[F[_]]:
  def create(user: User): F[User]
  def findByUsername(username: String): F[Option[User]]
  def findById(id: UserId): F[Option[User]]

object UserRepository:
  def make[F[_]: MonadCancelThrow](xa: Transactor[F]): UserRepository[F] =
    new UserRepository[F]:
      def create(user: User): F[User] =
        sql"""INSERT INTO users (id, username, email, password_hash, created_at)
              VALUES (${user.id}, ${user.username}, ${user.email}, ${user.passwordHash}, ${user.createdAt})
           """.update.run.transact(xa).as(user)

      def findByUsername(username: String): F[Option[User]] =
        sql"""SELECT id, username, email, password_hash, created_at FROM users
              WHERE username = $username""".query[User].option.transact(xa)

      def findById(id: UserId): F[Option[User]] =
        sql"""SELECT id, username, email, password_hash, created_at FROM users
              WHERE id = $id""".query[User].option.transact(xa)

trait TransactionRepository[F[_]]:
  def create(transaction: Transaction): F[Transaction]
  def findByUserId(userId: UserId): F[List[Transaction]]
  def findByUserIdAndDateRange(userId: UserId, from: LocalDateTime, to: LocalDateTime): F[List[Transaction]]
  def delete(id: TransactionId, userId: UserId): F[Boolean]

object TransactionRepository:
  def make[F[_]: MonadCancelThrow](xa: Transactor[F]): TransactionRepository[F] =
    new TransactionRepository[F]:
      def create(transaction: Transaction): F[Transaction] =
        sql"""INSERT INTO transactions (id, user_id, amount, transaction_type, category, description, date, created_at)
              VALUES (${transaction.id}, ${transaction.userId}, ${transaction.amount}, ${transaction.transactionType},
                      ${transaction.category}, ${transaction.description}, ${transaction.date}, ${transaction.createdAt})
           """.update.run.transact(xa).as(transaction)

      def findByUserId(userId: UserId): F[List[Transaction]] =
        sql"""SELECT id, user_id, amount, transaction_type, category, description, date, created_at
              FROM transactions WHERE user_id = $userId ORDER BY date DESC
           """.query[Transaction].to[List].transact(xa)

      def findByUserIdAndDateRange(userId: UserId, from: LocalDateTime, to: LocalDateTime): F[List[Transaction]] =
        sql"""SELECT id, user_id, amount, transaction_type, category, description, date, created_at
              FROM transactions WHERE user_id = $userId AND date >= $from AND date <= $to ORDER BY date DESC
           """.query[Transaction].to[List].transact(xa)

      def delete(id: TransactionId, userId: UserId): F[Boolean] =
        sql"""DELETE FROM transactions WHERE id = $id AND user_id = $userId
           """.update.run.transact(xa).map(_ > 0)
