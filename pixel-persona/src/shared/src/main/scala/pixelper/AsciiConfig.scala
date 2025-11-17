package pixelper

case class AsciiConfig(
  theme: Theme,
  width: Int = 64,
  height: Int = 64,
  dithering: Boolean = false,
  threshold: Double = 0.5
)
