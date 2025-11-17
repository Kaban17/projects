package pixelper

case class AvatarConfig(
  name: String,
  style: Style,
  symmetry: Symmetry,
  width: Int = 32,
  height: Int = 32
)
