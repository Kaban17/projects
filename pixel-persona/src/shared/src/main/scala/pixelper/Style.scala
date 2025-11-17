package pixelper

enum Style:
  case Monster, Robot, Planet

object Style:
  def fromString(s: String): Option[Style] = s.toLowerCase match
    case "monster" => Some(Monster)
    case "robot" => Some(Robot)
    case "planet" => Some(Planet)
    case _ => None
