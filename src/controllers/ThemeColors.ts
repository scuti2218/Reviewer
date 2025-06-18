import { BaseColorVariant } from "bootstrap-vue-next";

export const getThemeColor = (color: string) =>
  getComputedStyle(document.documentElement).getPropertyValue(`--bs-${color}`);

export const themeColors = Object.entries(
  "primary" as keyof BaseColorVariant
).reduce((acc, [key]) => {
  acc[key] = getThemeColor(key);
  return acc;
}, {} as Record<string, string>);
