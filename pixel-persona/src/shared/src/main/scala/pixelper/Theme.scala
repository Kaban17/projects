package pixelper

enum Theme:
  case Retro, Cyberpunk, Nature, Braille

object Theme:
  def fromString(s: String): Option[Theme] = s.toLowerCase match
    case "retro" => Some(Retro)
    case "cyberpunk" => Some(Cyberpunk)
    case "nature" => Some(Nature)
    case "braille" => Some(Braille)
    case _ => None
