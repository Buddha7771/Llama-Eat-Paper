from datetime import datetime
from enum import Enum
from dataclasses import dataclass

@dataclass
class PaperInfo:
    title: str
    authors: list[str]
    subjects: list[str]
    abstract: str
    submit: datetime
    pdf_url: str
    abs_url: str
    journal: str = None


class JournalIconUrl(Enum):
    arXiv = 'https://public.boxcloud.com/api/2.0/internal_files/780907538960/versions/834129875360/representations/png_paged_2048x2048/content/1.png?access_token=1!xF2vrQDxQQiAEhPq7CahaYq8U8g47H9qAXUyMIcWKx4pzj7R0V-HK7Oghlw5vpLUZYr1geoeYV64HtawqWWM7meX59JdH8fukVJRm8luHIN_1t7o4JgYcnvwJ6Qy0wXy-z4XagoLzeWLgsUcZMBFwecTrvFQ7HJdi36ve_pDBpQh7RMHlWzkxbsOwzSYtjsEi57JgmjzZwCanNdlWLgLEiLvIJWhqm4j0CwQUAkHM5v5Ahhg7m6pAmYaCXqIrYDpw3K7A-LeBnF2G1a1sgDvF42SOUfn_-PuqUV_iODMHP44mhiiP5j1dZvgg-bceKSrhCWM8jd_tXAFjPGyfVWnEpzpEy-sAaEGca4pJ99fEryCZGhla543NtyWPQDzu7227ZL5F6Fc0TfNvOc7JuMaLljHy-8jNdjrWiZlQZkgzxlIPT3GhVd_UuDE6URN2zy6vHUJtPN5GPbNVClwfjdxpuPDBhgebS9bkcF-AOd_ieCmiaD0u0xysET0olfNImW-pzJmLSk9POpwfKOJgp95HAGlJ2tIrbQhVygg8COjMIQDt4DVa3zWwU-UmgfX94EYZ_sOubw_tmmG0kNKv1MO-EFRbV8vcDJZ607ehBp6l6s.&shared_link=https%3A%2F%2Fcornell.app.box.com%2Fv%2Farxiv-logo-assets&box_client_name=box-content-preview&box_client_version=3.0.0'
    bioRxiv = 'https://ca.slack-edge.com/T04H68QRY5N-U087GQBCUS1-44b4a82a59e6-512'
