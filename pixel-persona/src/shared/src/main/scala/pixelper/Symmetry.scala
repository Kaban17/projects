package pixelper

enum Symmetry:
  case Vertical, Horizontal, Radial, Grid

object Symmetry:
  def fromString(s: String): Option[Symmetry] = s.toLowerCase match
    case "vertical" => Some(Vertical)
    case "horizontal" => Some(Horizontal)
    case "radial" => Some(Radial)
    case "grid" => Some(Grid)
    case _ => None
