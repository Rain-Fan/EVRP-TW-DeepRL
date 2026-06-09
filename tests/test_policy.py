import torch

from evrptw.core.simulator import RouteState, feasible_action_mask
from evrptw.data.io import load_instance
from evrptw.models import AttentionPolicy
from evrptw.models.features import dynamic_state_features, static_node_features


def test_policy_masks_infeasible_actions():
    instance = load_instance("data/samples/tiny_evrptw.json")
    state = RouteState.initial(instance)
    mask = torch.from_numpy(feasible_action_mask(instance, state))
    policy = AttentionPolicy(embedding_dim=32, num_heads=4, num_layers=1)

    logits = policy(
        static_node_features(instance),
        dynamic_state_features(instance, state),
        current_node=torch.tensor([0]),
        action_mask=mask,
    )

    assert logits.shape == (1, len(instance.nodes))
    assert torch.isfinite(logits[0, mask]).all()
    assert logits[0, 0] < -1e20

