"""Attention policy boundary for POMO/REINFORCE-style research."""

from __future__ import annotations

import torch
from torch import nn


class AttentionPolicy(nn.Module):
    def __init__(
        self,
        node_feature_dim: int = 9,
        state_feature_dim: int = 4,
        embedding_dim: int = 128,
        num_heads: int = 8,
        num_layers: int = 3,
    ) -> None:
        super().__init__()
        self.node_projection = nn.Linear(node_feature_dim, embedding_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dim,
            nhead=num_heads,
            dim_feedforward=embedding_dim * 4,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.state_projection = nn.Linear(state_feature_dim, embedding_dim)
        self.query_projection = nn.Linear(embedding_dim * 2, embedding_dim)
        self.scale = embedding_dim**-0.5

    def forward(
        self,
        node_features: torch.Tensor,
        state_features: torch.Tensor,
        current_node: torch.Tensor,
        action_mask: torch.Tensor,
    ) -> torch.Tensor:
        if node_features.ndim == 2:
            node_features = node_features.unsqueeze(0)
        if state_features.ndim == 1:
            state_features = state_features.unsqueeze(0)
        if action_mask.ndim == 1:
            action_mask = action_mask.unsqueeze(0)

        embeddings = self.encoder(self.node_projection(node_features))
        batch_indices = torch.arange(embeddings.size(0), device=embeddings.device)
        current = embeddings[batch_indices, current_node]
        dynamic = self.state_projection(state_features)
        query = self.query_projection(torch.cat((current, dynamic), dim=-1))
        logits = torch.einsum("bd,bnd->bn", query, embeddings) * self.scale
        return logits.masked_fill(~action_mask, torch.finfo(logits.dtype).min)
