# Engineering Handbook (Excerpt)

This excerpt covers on-call practices and the deployment process for
NorthwindOS, the software platform used across all Northwind Robotics
product tiers (Scout, Hauler, and Forge).

## Team structure

The engineering organization (~90 people, per the company overview) is split
into four groups:

- Platform team — owns NorthwindOS core services and the on-call rotation
  that handles Enterprise critical issues described in the support policy.
- Robotics firmware team — owns navigation, SLAM, and motor control software
  running on the physical units.
- Fleet software team — owns fleet tracking, optimization reports, and the
  Pro/Enterprise dashboards.
- Data & ML team — owns inventory-recognition models used by Scout's
  shelf-scanning feature.

## On-call rotation

The Platform team runs a weekly on-call rotation, 24/7, specifically to meet
the 1-hour critical response SLA for Forge (Enterprise) customers. On-call
engineers carry a pager and must acknowledge critical alerts within 15
minutes. Non-critical alerts are reviewed the next business day.

## Deployment process

NorthwindOS deploys follow a staged rollout:

1. Changes are merged to `main` after passing CI (unit tests, integration
   tests, and a security scan).
2. A canary deployment goes to 5% of Hauler and Forge fleets for 24 hours.
3. If error rates remain within normal bounds, the change rolls out to 100%
   of fleets over the next 48 hours.
4. Enterprise customers with custom integrations can opt into a "delayed
   rollout" track that lags the main rollout by one additional week, giving
   their teams time to test against the new version first.

## Incident response

Any incident that triggers the support policy's "Critical issue" definition
(a fully halted fleet) automatically pages the Platform on-call engineer and
opens an incident channel. The on-call engineer is responsible for the
initial response within the SLA window; the VP of Customer Success is looped
in for any incident affecting an Enterprise customer, since she may need to
communicate with the customer about escalation or refund exceptions.
