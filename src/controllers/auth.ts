import {
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  User,
  signInAnonymously,
} from "firebase/auth";
import { auth, provider } from "@services/firebase";
import { EventRadio } from "@controllers/EventChannel";

// Firebase Auth
export const loginWithGoogle = (showPrompt: boolean = true) => {
  provider.setCustomParameters({ prompt: showPrompt ? "select_account" : "" });
  return signInWithPopup(auth, provider);
};
export const loginAnonymous = () => signInAnonymously(auth);
export const logout = () => signOut(auth);
export const currentUser = () => auth.currentUser;
export function onFirebaseInitialize(): Promise<User | null> {
  return new Promise((resolve) => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      unsubscribe(); // stop listening after the first event
      resolve(user);
    });
  });
}

// Authentication Configs
export const AuthChannel = new EventRadio<IAuthData>("auth");
export const EAuthType = {
  Offline: "Offline",
  Anonymous: "Anonymous",
  Guest: "Guest",
  Google: "Google",
} as const;
export type EAuthType = (typeof EAuthType)[keyof typeof EAuthType];

export interface IAuthData {
  loggedIn: boolean;
  type: EAuthType | null;
  user: User | null;
  name: string;
}
export var defaultAuthData: IAuthData = {
  loggedIn: false as boolean,
  type: null as EAuthType | null,
  user: null as User | null,
  name: "" as string,
};

export type AuthTypeInfo = {
  title: string;
  icon?: string;
  details: string[];
  callback: () => Promise<any>;
  params?: Record<string, (...args: any[]) => boolean>;
};

export interface IAuthTypeContainerInfo {
  [key: string]: AuthTypeInfo;
}
const AuthTypeContainerInfo: IAuthTypeContainerInfo = {};
AuthTypeContainerInfo[EAuthType.Offline] = {
  title: EAuthType.Offline,
  details: [],
  callback: async () => {
    AuthChannel.transmit({
      loggedIn: true,
      type: EAuthType.Offline,
      user: null,
      name: EAuthType.Offline,
    });
  },
  params: {
    disableOnOffline: (_: boolean) => false,
  },
};
AuthTypeContainerInfo[EAuthType.Anonymous] = {
  title: EAuthType.Anonymous,
  details: [],
  callback: () =>
    loginAnonymous().then(() =>
      AuthChannel.transmit({
        loggedIn: true,
        type: EAuthType.Anonymous,
        user: null,
        name: EAuthType.Anonymous,
      })
    ),
  params: {
    disableOnOffline: (isOnline: boolean) => !isOnline,
  },
};
AuthTypeContainerInfo[EAuthType.Guest] = {
  title: EAuthType.Guest,
  details: [],
  callback: () =>
    loginAnonymous().then(() =>
      AuthChannel.transmit({
        loggedIn: true,
        type: EAuthType.Guest,
        user: null,
        name: EAuthType.Guest,
      })
    ),
  params: {
    disableOnOffline: (isOnline: boolean) => !isOnline,
  },
};
AuthTypeContainerInfo[EAuthType.Google] = {
  title: EAuthType.Google,
  details: [],
  callback: () =>
    loginWithGoogle().then((result) => {
      AuthChannel.transmit({
        loggedIn: true,
        type: EAuthType.Google,
        user: result.user,
        name: result.user.displayName ?? EAuthType.Google,
      });
    }),
  params: {
    disableOnOffline: (isOnline: boolean) => !isOnline,
  },
};

export { AuthTypeContainerInfo };
