package pixelper

import utest.*

object AvatarGeneratorTest extends TestSuite:
  val tests = Tests {
    test("generateSeed should create deterministic seed from name") {
      val seed1 = AvatarGenerator.generateSeed("alice")
      val seed2 = AvatarGenerator.generateSeed("alice")
      val seed3 = AvatarGenerator.generateSeed("bob")

      assert(seed1 == seed2)
      assert(seed1 != seed3)
    }

    test("generateAvatar should create SVG content") {
      val config = AvatarConfig("test", Style.Monster, Symmetry.Vertical)
      val svg = AvatarGenerator.generateAvatar(config)

      assert(svg.contains("<svg"))
      assert(svg.contains("test"))
    }

    test("Style.fromString should parse valid style names") {
      assert(Style.fromString("monster") == Some(Style.Monster))
      assert(Style.fromString("robot") == Some(Style.Robot))
      assert(Style.fromString("planet") == Some(Style.Planet))
      assert(Style.fromString("invalid") == None)
    }

    test("Symmetry.fromString should parse valid symmetry names") {
      assert(Symmetry.fromString("vertical") == Some(Symmetry.Vertical))
      assert(Symmetry.fromString("horizontal") == Some(Symmetry.Horizontal))
      assert(Symmetry.fromString("radial") == Some(Symmetry.Radial))
      assert(Symmetry.fromString("grid") == Some(Symmetry.Grid))
      assert(Symmetry.fromString("invalid") == None)
    }
  }
