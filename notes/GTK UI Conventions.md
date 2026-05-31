# GTK UI Conventions

Source: `mudlab/generic/views/__init__.py`, `mudlab/generic/views/glade/`

MudLab uses **GTK3 via PyGObject**. Every dialog is defined by a **Glade XML file** (`*.glade`) and loaded by a Python `View` class.

## View class hierarchy

```
mvc.View
  └── BaseView                  ← common helpers (layout mode, math widgets)
        ├── TitleView           ← adds set_title()
        │     └── FormattedTitleView
        ├── DialogView          ← wraps edit_dialog.glade; hosts a subview
        │     ├── ObjectListStoreView     ← left list + right editor panel
        │     └── ChildObjectListStoreView ← embedded version (no own window)
        └── InlineObjectListStoreView    ← compact list (layer/interlayer/relations boxes)
```

## Glade templates

| Template | Used by |
|---|---|
| `glade/edit_dialog.glade` | All `DialogView` subclasses — Edit Phase, Edit Mixture, Remove Background, Smooth Data, etc. Default size 1050×750. |
| `glade/object_store.glade` | Left list + right editor HPaned (Edit Phase Components tab) |
| `glade/inline_ols.glade` | Layer atoms, Interlayer atoms, Atom relations inline lists |
| `glade/lines/shift_dialog.glade` | Shift Pattern (has its own window, auto-sizes) |

## DialogView

`DialogView` loads `edit_dialog.glade` (a `GtkWindow`) then merges the subview's glade into `edit_child_box`. Subclasses set:
- `subview_builder` — path to the content glade
- `subview_toplevel` — widget ID of the content root
- `modal` — True/False
- `resizable` — True/False

Small tool dialogs (`BackgroundView`, `SmoothDataView`, `AddNoiseView`, `StripPeakView`, `CalculatePeakPropertiesView`, `TrimView`) call `set_default_size(-1, -1)` in `__init__` to cancel the 1050×750 default and auto-size to content, matching the Shift Pattern behaviour.

## Scrollbar policy

All scrolled windows use `overlay_scrolling=False` for **classic scrollbars** (beside content, not on top). Overlay scrollbars interfere with adjacent widgets (atom type dropdowns, pencil buttons).

```xml
<property name="vscrollbar_policy">automatic</property>
<property name="overlay_scrolling">False</property>
```

## Preventing over-tall spin boxes

When a `GtkSpinButton` shares a table row with a taller widget (e.g. the sample-button spanning 3 rows in `edit_marker.glade`), wrap it in `GtkAlignment` with `yscale=0` to keep it at natural (compact) height:

```xml
<object class="GtkAlignment">
  <property name="yalign">0.5</property>
  <property name="yscale">0</property>
  <child><object class="GtkSpinButton" .../></child>
</object>
```

## Window type hints

`type_hint=dialog` on GTK Windows causes Windows to suppress maximize/restore buttons. The main edit dialogs (`edit_dialog.glade`, `refine_results.glade`) do **not** set `type_hint`, giving a standard window decoration.

## Component list height

`object_store.glade`: `frm_objects_tv` has `vexpand=False`, `expand=False`, and the scrolled window uses `propagate_natural_height=True` + `max_content_height=300`. This keeps the component name list compact and prevents it from stretching when the right panel grows.

## Related Notes

- [[Architecture]]
- [[Phase and Component Model]]
- [[CIF Import]]
- [[Markers and Peak Detection]]
