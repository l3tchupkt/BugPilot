from __future__ import annotations

import typer

cli = typer.Typer(help="Manage and list Personas.")

@cli.callback(invoke_without_command=True)
def personas(ctx: typer.Context) -> None:
    """List all registered personas."""
    from bugpilot.personas.registry import PersonaRegistry
    
    PersonaRegistry.load_builtins()
    all_personas = PersonaRegistry.list_all()

    if not all_personas:
        typer.echo("No personas registered.")
        return

    typer.echo("Available Personas:")
    typer.echo("=" * 20)
    for p in all_personas:
        typer.echo(f"ID:          {p.id}")
        typer.echo(f"Name:        {p.name}")
        typer.echo(f"Description: {p.description}")
        typer.echo("-" * 20)
