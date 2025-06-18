import { EventRadio } from "@controllers/EventChannel";
import { BaseColorVariant } from "bootstrap-vue-next";

export interface IAlertData {
  message: string;
  timer?: number;
  variant?: keyof BaseColorVariant | null | undefined;
}

var alertChannels: Map<string, EventRadio<IAlertData>> = new Map();
export function useAlertChannel(key: string) {
  const keyID = "alert-" + key;
  const result = alertChannels.get(keyID) ?? new EventRadio<IAlertData>(keyID);
  alertChannels.set(keyID, result);
  return result;
}
