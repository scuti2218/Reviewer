import { ref as dbRef, onValue } from "firebase/database";
import { rdb } from "@/services/firebase";
import { EventRadio } from "./EventChannel";

export const FirebaseConnectivityChannel = new EventRadio<boolean>(
  "connectivity-firebase"
);
const connectedRef = dbRef(rdb, ".info/connected");
export function useFirebaseConnection() {
  onValue(connectedRef, (snapshot) =>
    FirebaseConnectivityChannel.transmit(!!snapshot.val(), "transmit")
  );
}
