import logging
from datetime import datetime, timezone, timedelta

import typer

from llama_eat_paper.tasks.daily import run_daily_task
from llama_eat_paper.tasks.conference import run_conference_task


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("run.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


app = typer.Typer(
    name="Llama-Eat-Paper",
    help="A CLI tool to find and notify about academic papers.",
)


@app.command()
def run_daily(
    delay: int = typer.Option(
        default=3,
        help="Number of days to look back for new papers.",
    ),
    threshold: float = typer.Option(
        default=0.8,
        help="Similarity threshold (0.0 to 1.0).",
    ),
    n_results: int = typer.Option(
        default=3,
        help="Number of max results to return for each query.",
    ),
):
    run_daily_task(
        start_date=datetime.now(timezone.utc) - timedelta(days=delay),
        end_date=datetime.now(timezone.utc) - timedelta(days=delay),
        threshold=threshold,
        n_results=n_results,
    )


@app.command()
def run_conference(
    conference: str = typer.Argument(
        ..., help="Conference name (e.g., ICLR.cc, ICML.cc)."
    ),
    year: int = typer.Argument(..., help="Year of the conference."),
    threshold: float = typer.Option(
        default=0.8,
        help="Similarity threshold (0.0 to 1.0).",
    ),
    n_results: int = typer.Option(
        default=3,
        help="Number of max results to return for each query.",
    ),
):
    run_conference_task(
        conference=conference,
        year=year,
        threshold=threshold,
        n_results=n_results,
    )
