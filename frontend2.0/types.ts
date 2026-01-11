// types.ts

export interface ClothingItem {
    id: string;
    imageUrl: string;
    type: "top" | "bottom" | "shoes" | "outerwear" | "accessories";
    colour: string;
    season: "spring" | "summer" | "fall" | "winter";
    occasion: string[];
}

export interface OutfitRequest {
    temperature: number;
    occasion: string;
    preferences: string[];
}

export interface OutfitResponse {
    outfit: {
        top?: ClothingItem;
        bottom?: ClothingItem;
        shoes?: ClothingItem;
        outerwear?: ClothingItem;
    };
    accessories: ClothingItem[];
    makeup: string;
    reasoning: string;
}