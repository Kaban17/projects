val scalaV = "3.6.2"

val utestVersion = "0.8.1"

ThisBuild / scalaVersion := scalaV
ThisBuild / organization := "com.pixelper"

lazy val sharedSettings = Seq(
  scalacOptions ++= Seq(
    "-encoding", "UTF-8",
    "-feature",
    "-unchecked",
    "-deprecation",
    "-language:implicitConversions",
    "-language:higherKinds",
    "-language:existentials",
    "-language:postfixOps"
  ),
  libraryDependencies ++= Seq(
    "com.lihaoyi" %%% "utest" % utestVersion % Test
  ),
  testFrameworks += new TestFramework("utest.runner.Framework")
)

lazy val shared = crossProject(JSPlatform, JVMPlatform)
  .in(file("src/shared"))
  .settings(sharedSettings)
  .jvmSettings(
    // JVM-specific settings
  )
  .jsSettings(
    // JS-specific settings
  )

lazy val sharedJVM = shared.jvm
lazy val sharedJS = shared.js

lazy val jvm = (project in file("src/jvm"))
  .settings(sharedSettings)
  .settings(
    name := "pixel-persona-jvm"
  )
  .dependsOn(sharedJVM)

lazy val js = (project in file("src/js"))
  .settings(sharedSettings)
  .settings(
    name := "pixel-persona-js",
    scalaJSUseMainModuleInitializer := true,
    libraryDependencies ++= Seq(
      "io.indigoengine" %%% "tyrian" % "0.12.0"
    )
  )
  .enablePlugins(ScalaJSPlugin)
  .dependsOn(sharedJS)
