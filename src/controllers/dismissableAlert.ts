import { EventRadio } from "@controllers/EventChannel";

export interface IDismissableAlert {
  show: boolean;
  message: string;
}

export const dismissableAlertChannel = new EventRadio<IDismissableAlert>(
  "dismissable-alert"
);
