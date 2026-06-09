# EVRP-TW Problem Formulation

## Sets

- depot: node `0`;
- customers: nodes requiring exactly one service;
- charging stations: optional intermediate nodes;
- homogeneous electric vehicles.

## State

At each construction step the state contains:

- current node and current route;
- elapsed route time;
- remaining payload capacity;
- remaining battery energy;
- customers already served;
- number of vehicles used.

## Feasibility

An action is feasible only when:

1. the target customer has not already been served;
2. customer demand does not exceed remaining vehicle capacity;
3. travel energy does not exceed the remaining battery;
4. service starts no later than the target node's due time;
5. a new route does not exceed the available fleet.

Waiting is allowed when a vehicle reaches a node before its ready time. A
charging-station visit restores the battery to full and adds charging time.

## Objective

The initial objective is total travel distance subject to feasibility. Future
experiments may add weighted vehicle count, charging time, lateness penalties,
or energy cost, but each component must be reported separately.

## Current Simplifications

- energy consumption is linear in distance;
- charging is linear and always restores a full battery;
- vehicles are homogeneous;
- each route starts independently at the depot's ready time;
- stochastic travel and partial charging are not yet modeled.

These assumptions are explicit extension points, not claims about real fleets.

