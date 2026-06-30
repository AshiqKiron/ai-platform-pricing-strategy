# The Problem with Legacy Pricing

## The "Raw Compute" Fallacy
Legacy cloud providers and basic GPU clouds (like early RunPod) price purely on **$/GPU-hour** or **$/TB**. This model is fundamentally broken for modern AI workloads because it misaligns provider revenue with customer success.

## Why $/GPU-Hour Fails
1. **The Idle Tax:** If a customer pays for an A100 for $2.00/hour, but the GPU is idle for 20% of the time waiting for data to load from storage or batching inference requests, they are effectively paying $2.50/hour for *actual* compute. 
2. **The Blame Game:** When TCO balloons due to idle time, customers don't blame their own inefficient data pipelines; they blame the cloud provider's "expensive compute."
3. **Inference Inefficiency:** For inference, traffic is bursty. Paying for 24/7 GPU uptime for a model that only gets 100 requests a day is a massive waste of capital.

## Conclusion
Pricing must shift from **Provisioned Capacity** to **Efficient Outcomes**.