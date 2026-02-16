import { API_BASE } from "./config";
import type { PredictionDTO } from "./types";
import type { TreeDTO } from "./types";


export async function getPrediction(
    featureValues: number[],
    tree: TreeDTO
): Promise<PredictionDTO> {
    const res = await fetch(`${API_BASE}/api/predict`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ x: featureValues, tree }),
    });
    if (!res.ok) {
        throw new Error(`Prediction failed: ${res.status}`);
    }
    const jsonResponse = await res.json();
    console.log("Received prediction response:", jsonResponse);
    return jsonResponse as Promise<PredictionDTO>;
}