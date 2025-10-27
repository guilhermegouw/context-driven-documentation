"""CLI entry point for cddoc."""

import click


@click.group()
@click.version_option()
def main():
    """Context-Driven Documentation CLI."""
    pass


@main.command()
@click.argument('path', default='.')
def init(path):
    """Initialize CDD structure in a project."""
    click.echo(f"🚀 Initializing CDD in {path}...")
    click.echo("🚧 Coming soon - use /init-command in Claude Code to build this!")


if __name__ == '__main__':
    main()
