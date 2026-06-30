# Proposed "Efficiency-Aligned" Packaging

We propose a 3-tier model that aligns our pricing with the customer's actual stage of the AI lifecycle.

## Tier 1: Dev/Sandbox (The Hook)
* **Model:** Standard $/GPU-hour.
* **Target:** Individual researchers, students, early-stage devs.
* **Why it works:** Low friction. Developers want predictable, simple billing while experimenting. High margin for us, as sandbox utilization is naturally low.

## Tier 2: Production/Inference (The Scale)
* **Model:** Serverless / Scale-to-Zero. Priced per 1,000 tokens or per inference request.
* **Target:** Deployed AI applications, SaaS products.
* **The ROI Pitch:** *"You only pay when your model is actually working."* 
* **Why it works:** Mirrors Modal/Replicate. Eliminates the "idle tax" for bursty inference traffic. We absorb the cold-start latency; they absorb zero infrastructure management costs.

## Tier 3: Enterprise Training (The Margin)
* **Model:** Managed Spot/Preemptible Optimization. Priced at a 20-30% premium over raw spot instances, but includes automated checkpointing and resumption SLAs.
* **Target:** LLM fine-tuning, large-scale model training.
* **The ROI Pitch:** *"We make cheap, unreliable GPUs as reliable as expensive on-demand GPUs, cutting your training TCO by 60%."*
* **Why it works:** Training is highly fault-tolerant but time-sensitive. By handling the complex engineering of spot-interruptions automatically, we unlock massive savings for the client while maintaining high margins for ourselves.