package pixelper

object AsciiArtGenerator:
  def generateAsciiArt(imageData: Array[Array[Double]], config: AsciiConfig): String =
    val themeChars = getThemeCharacters(config.theme)
    val charCount = themeChars.length
    val step = 1.0 / charCount

    val asciiArt = imageData.map { row =>
      row.map { pixel =>
        val index = math.min((pixel / step).toInt, charCount - 1)
        themeChars.charAt(index)
      }.mkString
    }.mkString("\n")

    applySymmetry(asciiArt, config)

  def applySymmetry(asciiArt: String, config: AsciiConfig): String =
    // Пока что просто возвращаем оригинальный ASCII-арт
    // Позже добавим реализацию симметрии
    asciiArt

  private def getThemeCharacters(theme: Theme): String = theme match
    case Theme.Retro => "@%#*+=-:."
    case Theme.Cyberpunk => "⌁⌇⌖▮◈▯⌗⎍⏎"
    case Theme.Nature => "🌿🍃🌲☁💧⛰☀🌙"
    case Theme.Braille => "⣿⣶⣤⣄⣀⡀⢀⢠⢰⢸⣀⣄⣤⣶⣿"
