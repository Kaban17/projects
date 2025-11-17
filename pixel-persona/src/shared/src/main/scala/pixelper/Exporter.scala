package pixelper

object Exporter:
  def exportToTxt(asciiArt: String): String =
    asciiArt

  def exportToAnsi(asciiArt: String, theme: Theme): String =
    // Простая реализация ANSI экспорта
    // В реальной реализации нужно добавить цвета
    asciiArt

  def exportToSvg(asciiArt: String, width: Int, height: Int): String =
    s"""<svg width="$width" height="$height" xmlns="http://www.w3.org/2000/svg">
       <text x="0" y="10" font-family="monospace" font-size="10">
         ${asciiArt.replace("\n", "<tspan x=\"0\" dy=\"10\">").replace("\n", "</tspan>")}
       </text>
     </svg>"""

  def exportToJson(config: AvatarConfig | AsciiConfig): String =
    // В реальной реализации нужно сериализовать конфигурацию в JSON
    config.toString

  def exportToPng(asciiArt: String): Array[Byte] =
    // В реальной реализации нужно конвертировать ASCII-арт в PNG
    Array.empty[Byte]
