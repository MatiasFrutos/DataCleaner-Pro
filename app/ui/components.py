"""
Componentes reutilizables de DataCleaner Pro.

Contiene tarjetas, botones, badges y bloques visuales usados
por distintas pantallas de la aplicación.
"""

import customtkinter as ctk

from app.ui.styles import COLORS, FONTS, SIZES


class AppCard(ctk.CTkFrame):
    """
    Tarjeta base reutilizable.
    """

    def __init__(self, master, title=None, subtitle=None, **kwargs):
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", COLORS["surface"]),
            corner_radius=kwargs.pop("corner_radius", SIZES["radius_lg"]),
            border_width=kwargs.pop("border_width", 1),
            border_color=kwargs.pop("border_color", COLORS["border_soft"]),
            **kwargs
        )

        self.grid_columnconfigure(0, weight=1)

        current_row = 0

        if title:
            self.title_label = ctk.CTkLabel(
                self,
                text=title,
                font=FONTS["subtitle"],
                text_color=COLORS["text"],
                anchor="w",
            )
            self.title_label.grid(
                row=current_row,
                column=0,
                sticky="ew",
                padx=18,
                pady=(16, 2),
            )
            current_row += 1

        if subtitle:
            self.subtitle_label = ctk.CTkLabel(
                self,
                text=subtitle,
                font=FONTS["body"],
                text_color=COLORS["text_muted"],
                anchor="w",
                wraplength=420,
                justify="left",
            )
            self.subtitle_label.grid(
                row=current_row,
                column=0,
                sticky="ew",
                padx=18,
                pady=(0, 16),
            )


class StatCard(ctk.CTkFrame):
    """
    Tarjeta pequeña para métricas o estados.
    """

    def __init__(self, master, label, value, helper=None, accent="primary", **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["surface"],
            corner_radius=SIZES["radius_lg"],
            border_width=1,
            border_color=COLORS["border_soft"],
            **kwargs
        )

        self.grid_columnconfigure(0, weight=1)

        accent_color = COLORS.get(accent, COLORS["primary"])

        self.label = ctk.CTkLabel(
            self,
            text=label,
            font=FONTS["small_bold"],
            text_color=COLORS["text_muted"],
            anchor="w",
        )
        self.label.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 2))

        self.value = ctk.CTkLabel(
            self,
            text=value,
            font=FONTS["title"],
            text_color=accent_color,
            anchor="w",
        )
        self.value.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 2))

        self.helper = ctk.CTkLabel(
            self,
            text=helper or "",
            font=FONTS["small"],
            text_color=COLORS["text_faint"],
            anchor="w",
        )
        self.helper.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 14))


class AppButton(ctk.CTkButton):
    """
    Botón primario reutilizable.
    """

    def __init__(self, master, text, command=None, variant="primary", **kwargs):
        colors = {
            "primary": {
                "fg_color": COLORS["primary"],
                "hover_color": COLORS["primary_hover"],
                "text_color": "#ffffff",
            },
            "secondary": {
                "fg_color": COLORS["surface_muted"],
                "hover_color": COLORS["border"],
                "text_color": COLORS["text"],
            },
            "danger": {
                "fg_color": COLORS["danger"],
                "hover_color": "#b91c1c",
                "text_color": "#ffffff",
            },
        }

        selected = colors.get(variant, colors["primary"])

        super().__init__(
            master,
            text=text,
            command=command,
            height=40,
            corner_radius=SIZES["radius_md"],
            font=FONTS["button"],
            fg_color=selected["fg_color"],
            hover_color=selected["hover_color"],
            text_color=selected["text_color"],
            **kwargs
        )


class Badge(ctk.CTkLabel):
    """
    Badge visual para estados.
    """

    def __init__(self, master, text, variant="primary", **kwargs):
        palette = {
            "primary": (COLORS["primary_soft"], COLORS["primary"]),
            "success": (COLORS["success_soft"], COLORS["success"]),
            "warning": (COLORS["warning_soft"], COLORS["warning"]),
            "danger": (COLORS["danger_soft"], COLORS["danger"]),
            "muted": (COLORS["surface_muted"], COLORS["text_muted"]),
        }

        bg, fg = palette.get(variant, palette["primary"])

        super().__init__(
            master,
            text=text,
            fg_color=bg,
            text_color=fg,
            font=FONTS["small_bold"],
            corner_radius=999,
            padx=10,
            pady=4,
            **kwargs
        )


class EmptyState(ctk.CTkFrame):
    """
    Estado vacío reutilizable para pantallas sin datos.
    """

    def __init__(self, master, title, message, action_text=None, action_command=None, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["surface"],
            corner_radius=SIZES["radius_xl"],
            border_width=1,
            border_color=COLORS["border_soft"],
            **kwargs
        )

        self.grid_columnconfigure(0, weight=1)

        self.icon = ctk.CTkLabel(
            self,
            text="◆",
            font=("Segoe UI", 34, "bold"),
            text_color=COLORS["primary"],
        )
        self.icon.grid(row=0, column=0, pady=(28, 6))

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=FONTS["title"],
            text_color=COLORS["text"],
        )
        self.title_label.grid(row=1, column=0, padx=24, pady=(0, 6))

        self.message_label = ctk.CTkLabel(
            self,
            text=message,
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
            wraplength=520,
            justify="center",
        )
        self.message_label.grid(row=2, column=0, padx=24, pady=(0, 18))

        if action_text:
            self.action_button = AppButton(
                self,
                text=action_text,
                command=action_command,
            )
            self.action_button.grid(row=3, column=0, pady=(0, 28))