// This mirrors the backend response EXACTLY
export type TreeDTO = {
    root_id: number | null;
    nodes: Record<number, TreeNodeDTO>;
    edges: Record<string, TreeEdgeDTO>;
    metrics: MetricsDTO;
    feature_names: string[];
    label_names: string[];

}

export type TreeNodeDTO = {
    id: number;
    feature?: number | null;
    threshold?: number | null;
    value?: number | null;
    information_gain?: number | null;
    is_leaf: boolean;
    samples?: number[] | Record<string, number>;
    depth?: number;
    predicted_class?: number | null;
    left_child?: number | null;
    right_child?: number | null;
};

export type TreeEdgeDTO = {
    source: number;
    target: number;
    branch: string;
    operator: string;
    feature: number;
    threshold: number;
};

export type MetricsDTO = {
    accuracy: number | null;
    precision: number | null;
    recall: number | null;
    f1_score: number | null;
}

export type PredictionDTO = {
    predicted_class: number;
    path: number[];
};