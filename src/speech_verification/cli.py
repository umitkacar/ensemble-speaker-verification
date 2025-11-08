"""Command-line interface for speech verification."""

import json
import logging
import sys
from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.logging import RichHandler
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table

    CLI_AVAILABLE = True
except ImportError as e:
    CLI_AVAILABLE = False
    _MISSING_DEPENDENCY = str(e)

    # Create dummy app for graceful degradation
    class DummyApp:
        def __init__(self, *args, **kwargs):
            pass

        def command(self, *args, **kwargs):
            def decorator(func):
                return func

            return decorator

        def __call__(self, *args, **kwargs):
            raise ImportError(
                f"CLI dependencies not installed: {_MISSING_DEPENDENCY}\n"
                f"Install with: pip install speech-verification-ensemble[all]"
            )

    app = DummyApp()
    Console = type("Console", (), {"print": print})
    console = Console()

if CLI_AVAILABLE:
    from speech_verification import __version__
    from speech_verification.config import Config, VerificationConfig
    from speech_verification.core.cnn import CNNVerifier
    from speech_verification.core.fusion import EnsembleVerifier
    from speech_verification.core.mfcc import MFCCVerifier
    from speech_verification.utils.audio import convert_audio, record_audio

    # Initialize Typer app
    app = typer.Typer(
        name="speech-verify",
        help="🎙️  Speech Verification Ensemble - Multi-modal speaker verification",
        add_completion=True,
        rich_markup_mode="rich",
    )

    console = Console()


    def setup_logging(verbose: bool = False) -> None:
        """Setup logging configuration."""
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(message)s",
            handlers=[RichHandler(console=console, rich_tracebacks=True)],
        )


    @app.command()
    def version() -> None:
        """Show version information."""
        console.print(f"[bold cyan]Speech Verification Ensemble[/bold cyan] v{__version__}")
        console.print("[dim]Multi-modal speaker verification system[/dim]")


    @app.command()
    def verify(
        audio1: Path = typer.Argument(..., help="First audio file", exists=True),
        audio2: Path = typer.Argument(..., help="Second audio file", exists=True),
        method: str = typer.Option(
            "ensemble",
            "--method",
            "-m",
            help="Verification method: mfcc, cnn, or ensemble",
        ),
        device: str = typer.Option(
            "cpu", "--device", "-d", help="Device to use: cpu or cuda"
        ),
        verbose: bool = typer.Option(
            False, "--verbose", "-v", help="Enable verbose output"
        ),
        json_output: bool = typer.Option(
            False, "--json", "-j", help="Output results as JSON"
        ),
    ) -> None:
        """
        Verify if two audio files are from the same speaker.

        [bold cyan]Examples:[/bold cyan]

            # Using ensemble method (recommended)
            speech-verify verify speaker1.wav speaker2.wav

            # Using only MFCC
            speech-verify verify audio1.wav audio2.wav --method mfcc

            # Using CNN with GPU
            speech-verify verify audio1.wav audio2.wav --method cnn --device cuda
        """
        setup_logging(verbose)

        config = Config()
        config.verification.device = device

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("🔍 Verifying speakers...", total=None)

                if method == "mfcc":
                    verifier = MFCCVerifier(verification_config=config.verification)
                    result = verifier.verify(audio1, audio2, return_distance=True)
                    is_same, distance = result

                    if json_output:
                        output = {
                            "method": "mfcc",
                            "is_same_speaker": bool(is_same),
                            "distance": float(distance),
                            "threshold": verifier.threshold,
                        }
                        console.print_json(data=output)
                    else:
                        _print_result(
                            is_same, f"MFCC Distance: {distance:.2f}", method
                        )

                elif method == "cnn":
                    verifier = CNNVerifier(verification_config=config.verification)
                    result = verifier.verify(audio1, audio2, return_distance=True)
                    is_same, distance = result

                    if json_output:
                        output = {
                            "method": "cnn",
                            "is_same_speaker": bool(is_same),
                            "distance": float(distance),
                            "threshold": verifier.threshold,
                        }
                        console.print_json(data=output)
                    else:
                        _print_result(
                            is_same, f"CNN Distance: {distance:.4f}", method
                        )

                elif method == "ensemble":
                    verifier = EnsembleVerifier(verification_config=config.verification)
                    result = verifier.verify(audio1, audio2, return_details=True)

                    if json_output:
                        console.print_json(data=result)
                    else:
                        _print_ensemble_result(result)

                else:
                    console.print(
                        f"[bold red]❌ Unknown method: {method}[/bold red]"
                    )
                    raise typer.Exit(1)

                progress.update(task, completed=True)

        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
            raise typer.Exit(1)


    @app.command()
    def record(
        output: Path = typer.Argument(..., help="Output audio file path"),
        duration: int = typer.Option(5, "--duration", "-d", help="Recording duration (seconds)"),
        sample_rate: int = typer.Option(16000, "--sr", help="Sample rate"),
    ) -> None:
        """
        Record audio from microphone.

        [bold cyan]Example:[/bold cyan]

            speech-verify record my_voice.wav --duration 10
        """
        setup_logging()

        try:
            console.print(f"[yellow]🎤 Recording for {duration} seconds...[/yellow]")
            console.print("[dim]Speak into your microphone...[/dim]")

            record_audio(output, duration=duration, sr=sample_rate)

            console.print(f"[green]✅ Audio saved to {output}[/green]")

        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
            raise typer.Exit(1)


    @app.command()
    def convert(
        input_file: Path = typer.Argument(..., help="Input audio file", exists=True),
        output_file: Path = typer.Argument(..., help="Output audio file"),
        sample_rate: int = typer.Option(16000, "--sr", help="Target sample rate"),
    ) -> None:
        """
        Convert audio file to different format/sample rate.

        [bold cyan]Example:[/bold cyan]

            speech-verify convert input.mp3 output.wav --sr 16000
        """
        setup_logging()

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("🔄 Converting audio...", total=None)

                convert_audio(input_file, output_file, sr=sample_rate)

                progress.update(task, completed=True)

            console.print(f"[green]✅ Converted {input_file} -> {output_file}[/green]")

        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
            raise typer.Exit(1)


    @app.command()
    def batch(
        pairs_file: Path = typer.Argument(
            ..., help="JSON file with audio pairs", exists=True
        ),
        method: str = typer.Option(
            "ensemble", "--method", "-m", help="Verification method"
        ),
        output: Optional[Path] = typer.Option(
            None, "--output", "-o", help="Output results file"
        ),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    ) -> None:
        """
        Batch verification of multiple audio pairs.

        The pairs file should be JSON format:
        [
            ["audio1.wav", "audio2.wav"],
            ["audio3.wav", "audio4.wav"]
        ]

        [bold cyan]Example:[/bold cyan]

            speech-verify batch pairs.json --method ensemble --output results.json
        """
        setup_logging(verbose)

        try:
            # Load pairs
            with open(pairs_file) as f:
                pairs = json.load(f)

            console.print(f"[cyan]📋 Processing {len(pairs)} audio pairs...[/cyan]")

            config = Config()

            # Initialize verifier
            if method == "mfcc":
                verifier = MFCCVerifier(verification_config=config.verification)
                results = verifier.batch_verify(pairs)
                results = [
                    {"is_same_speaker": r[0], "distance": r[1]} for r in results
                ]

            elif method == "cnn":
                verifier = CNNVerifier(verification_config=config.verification)
                results = verifier.batch_verify(pairs)
                results = [
                    {"is_same_speaker": r[0], "distance": r[1]} for r in results
                ]

            elif method == "ensemble":
                verifier = EnsembleVerifier(verification_config=config.verification)
                results = verifier.batch_verify(pairs)

            else:
                console.print(f"[bold red]❌ Unknown method: {method}[/bold red]")
                raise typer.Exit(1)

            # Output results
            if output:
                with open(output, "w") as f:
                    json.dump(results, f, indent=2)
                console.print(f"[green]✅ Results saved to {output}[/green]")
            else:
                console.print_json(data=results)

            # Summary
            same_count = sum(1 for r in results if r["is_same_speaker"])
            console.print(
                f"\n[cyan]📊 Summary: {same_count}/{len(results)} "
                f"pairs verified as same speaker[/cyan]"
            )

        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
            raise typer.Exit(1)


    @app.command()
    def benchmark(
        data_dir: Path = typer.Argument(..., help="Directory with audio files", exists=True),
        method: str = typer.Option("ensemble", "--method", "-m", help="Method to benchmark"),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    ) -> None:
        """
        Benchmark verification methods on a dataset.

        [bold cyan]Example:[/bold cyan]

            speech-verify benchmark ./test_data --method ensemble
        """
        setup_logging(verbose)

        console.print("[yellow]⏱️  Benchmarking not yet implemented[/yellow]")
        console.print("[dim]Coming soon![/dim]")


    def _print_result(is_same: bool, details: str, method: str) -> None:
        """Print verification result."""
        table = Table(title="Verification Result", show_header=True)
        table.add_column("Method", style="cyan")
        table.add_column("Result", style="bold")
        table.add_column("Details", style="dim")

        result_text = "[green]✅ Same Speaker[/green]" if is_same else "[red]❌ Different Speaker[/red]"
        table.add_row(method.upper(), result_text, details)

        console.print(table)


    def _print_ensemble_result(result: dict) -> None:
        """Print ensemble verification result."""
        table = Table(title="Ensemble Verification Result", show_header=True)
        table.add_column("Component", style="cyan")
        table.add_column("Result", style="bold")
        table.add_column("Distance", justify="right")
        table.add_column("Normalized", justify="right")

        # MFCC row
        mfcc_result = "✅" if result["mfcc"]["result"] else "❌"
        table.add_row(
            "MFCC + DTW",
            mfcc_result,
            f"{result['mfcc']['distance']:.2f}",
            f"{result['mfcc']['normalized']:.4f}",
        )

        # CNN row
        cnn_result = "✅" if result["cnn"]["result"] else "❌"
        table.add_row(
            "CNN (Resemblyzer)",
            cnn_result,
            f"{result['cnn']['distance']:.4f}",
            f"{result['cnn']['normalized']:.4f}",
        )

        # Fusion row
        fusion_result = (
            "[green]✅ Same Speaker[/green]"
            if result["is_same_speaker"]
            else "[red]❌ Different Speaker[/red]"
        )
        table.add_row(
            "[bold]Ensemble Fusion[/bold]",
            fusion_result,
            f"[bold]{result['fusion_score']:.4f}[/bold]",
            "-",
        )

        console.print(table)

        # Additional info
        console.print(
            f"\n[dim]Fusion weights: CNN={result['weights']['cnn']}, "
            f"MFCC={result['weights']['mfcc']}[/dim]"
        )


    def main() -> None:
        """Main entry point."""
        app()


    if __name__ == "__main__":
        main()

else:
    def setup_logging(verbose: bool = False) -> None:
        """Dummy setup_logging when CLI not available."""
        pass

    def main():
        """Main entry point."""
        raise ImportError(
            "CLI dependencies not installed. "
            "Install with: pip install speech-verification-ensemble[all]"
        )
