package pixelper

import tyrian.*
import tyrian.Html.*
import tyrian.SVG.*

enum Msg:
  case NameChanged(name: String)
  case StyleChanged(style: String)
  case SymmetryChanged(symmetry: String)
  case ThemeChanged(theme: String)
  case GenerateAvatar
  case NoOp

case class Model(
    name: String = "Pixel",
    style: String = "Monster",
    symmetry: String = "Vertical",
    theme: String = "Retro",
    avatarSvg: String = "",
    asciiArt: String = ""
)

object MainApp extends TyrianApp[Msg, Model]:

  def init(flags: Map[String, String]): (Model, Cmd[Msg]) =
    val initialModel = Model()
    (initialModel, Cmd.None)

  def update(model: Model, msg: Msg): (Model, Cmd[Msg]) =
    msg match
      case Msg.NameChanged(name) =>
        (model.copy(name = name), Cmd.None)

      case Msg.StyleChanged(styleStr) =>
        (model.copy(style = styleStr), Cmd.None)

      case Msg.SymmetryChanged(symmetryStr) =>
        (model.copy(symmetry = symmetryStr), Cmd.None)

      case Msg.ThemeChanged(themeStr) =>
        (model.copy(theme = themeStr), Cmd.None)

      case Msg.GenerateAvatar =>
        (model, Cmd.None)

      case Msg.NoOp =>
        (model, Cmd.None)

  def view(model: Model): Html[Msg] =
    div(
      h1("PixelPersona - Генератор аватаров"),
      div(
        label("Имя: "),
        input(
          placeholder := "Введите имя",
          onInput(name => Msg.NameChanged(name)),
          value := model.name
        )
      ),
      div(
        label("Стиль: "),
        select(
          onChange(style => Msg.StyleChanged(style)),
          value := model.style,
          Option("Monster", "Monster"),
          Option("Robot", "Robot"),
          Option("Planet", "Planet")
        )
      ),
      div(
        label("Симметрия: "),
        select(
          onChange(symmetry => Msg.SymmetryChanged(symmetry)),
          value := model.symmetry,
          Option("Vertical", "Vertical"),
          Option("Horizontal", "Horizontal"),
          Option("Radial", "Radial"),
          Option("Grid", "Grid")
        )
      ),
      div(
        label("Тема: "),
        select(
          onChange(theme => Msg.ThemeChanged(theme)),
          value := model.theme,
          Option("Retro", "Retro"),
          Option("Cyberpunk", "Cyberpunk"),
          Option("Nature", "Nature"),
          Option("Braille", "Braille")
        )
      ),
      button(onClick(Msg.GenerateAvatar))("Сгенерировать"),
      div(
        h2("Аватар:"),
        raw("<svg width='100' height='100'><rect width='100%' height='100%' fill='#4CAF50'/><text x='50%' y='50%' font-family='monospace' font-size='12' text-anchor='middle' dy='.3em'>PIX</text></svg>")
      ),
      div(
        h2("ASCII-арт:"),
        pre("@%#*+=-:.")
      )
    )

  def subscriptions(model: Model): Sub[Msg] =
    Sub.None
