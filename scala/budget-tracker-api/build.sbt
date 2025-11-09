name := "budget-tracker-api"
version := "0.1.0"
scalaVersion := "3.3.1"

val http4sVersion = "0.23.23"
val doobieVersion = "1.0.0-RC4"
val circeVersion = "0.14.6"
val catsEffectVersion = "3.5.2"

libraryDependencies ++= Seq(
  // HTTP4s
  "org.http4s" %% "http4s-dsl" % http4sVersion,
  "org.http4s" %% "http4s-ember-server" % http4sVersion,
  "org.http4s" %% "http4s-ember-client" % http4sVersion,
  "org.http4s" %% "http4s-circe" % http4sVersion,

  // Doobie
  "org.tpolecat" %% "doobie-core" % doobieVersion,
  "org.tpolecat" %% "doobie-postgres" % doobieVersion,
  "org.tpolecat" %% "doobie-hikari" % doobieVersion,

  // Circe (JSON)
  "io.circe" %% "circe-core" % circeVersion,
  "io.circe" %% "circe-generic" % circeVersion,
  "io.circe" %% "circe-parser" % circeVersion,

  // Cats Effect
  "org.typelevel" %% "cats-effect" % catsEffectVersion,

  // Logging
  "org.typelevel" %% "log4cats-slf4j" % "2.6.0",
  "ch.qos.logback" % "logback-classic" % "1.4.11",

  // Password hashing - используем Java библиотеку напрямую
  "org.mindrot" % "jbcrypt" % "0.4"
)

scalacOptions ++= Seq(
  "-encoding", "UTF-8",
  "-feature",
  "-language:higherKinds",
  "-deprecation"
)
