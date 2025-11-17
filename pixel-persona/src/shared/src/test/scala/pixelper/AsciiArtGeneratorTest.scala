package pixelper

import utest.*

object AsciiArtGeneratorTest extends TestSuite:
  val tests = Tests {
    test("generateAsciiArt should create ASCII art from image data") {
      val imageData = Array(
        Array(0.0, 0.5, 1.0),
        Array(1.0, 0.5, 0.0),
        Array(0.5, 0.0, 1.0)
      )

      val config = AsciiConfig(Theme.Retro)
      val asciiArt = AsciiArtGenerator.generateAsciiArt(imageData, config)

      assert(asciiArt.nonEmpty)
      assert(asciiArt.linesIterator.size == 3)
    }

    test("getThemeCharacters should return correct characters for each theme") {
      assert(AsciiArtGenerator.getThemeCharacters(Theme.Retro).nonEmpty)
      assert(AsciiArtGenerator.getThemeCharacters(Theme.Cyberpunk).nonEmpty)
      assert(AsciiArtGenerator.getThemeCharacters(Theme.Nature).nonEmpty)
      assert(AsciiArtGenerator.getThemeCharacters(Theme.Braille).nonEmpty)
    }

    test("Theme.fromString should parse valid theme names") {
      assert(Theme.fromString("retro") == Some(Theme.Retro))
      assert(Theme.fromString("cyberpunk") == Some(Theme.Cyberpunk))
      assert(Theme.fromString("nature") == Some(Theme.Nature))
      assert(Theme.fromString("braille") == Some(Theme.Braille))
      assert(Theme.fromString("invalid") == None)
    }
  }
