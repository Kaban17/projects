package pixelper

import scala.util.hashing.MurmurHash3

object AvatarGenerator:
  def generateSeed(name: String): Long =
    MurmurHash3.stringHash(name).toLong

  def generateAvatar(config: AvatarConfig): String =
    // Простая реализация генерации SVG аватара
    val seed = generateSeed(config.name)
    val svgContent = s"""<svg width="${config.width}" height="${config.height}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#${seedToColor(seed)}"/>
      <text x="50%" y="50%" font-family="monospace" font-size="12" text-anchor="middle" dy=".3em">
        ${config.name.take(3)}
      </text>
    </svg>"""
    svgContent

  private def seedToColor(seed: Long): String =
    // Преобразование seed в цвет в формате hex
    val r = (seed & 0xFF0000) >> 16
    val g = (seed & 0x00FF00) >> 8
    val b = seed & 0x0000FF
    f"${r}%02x${g}%02x${b}%02x"
