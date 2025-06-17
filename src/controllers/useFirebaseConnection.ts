import { ref as dbRef, onValue } from "firebase/database";
import { rdb } from "@/services/firebase";
import { EventRadio } from "./EventChannel";

export const FirebaseConnectivityChannel = new EventRadio<boolean>(
  "connectivity-firebase"
);
var lastNetworkCheck: boolean | undefined = undefined;
export function useFirebaseConnection() {
  onValue(dbRef(rdb, ".info/connected"), (snapshot) => {
    const newNetworkCheck = !!snapshot.val();
    if (lastNetworkCheck !== newNetworkCheck) {
      FirebaseConnectivityChannel.transmit(newNetworkCheck, "transmit");
      lastNetworkCheck = newNetworkCheck;
      console.log(
        "Firebase Connection: " +
          (newNetworkCheck ? "Connected" : "Disconnected")
      );
    }
  });
}
