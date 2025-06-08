import {
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  User,
} from "firebase/auth";
import { auth, provider } from "@services/firebase";
import { EventRadio } from "@controllers/EventChannel";

// Firebase Auth
export const login = () => signInWithPopup(auth, provider);
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
export const EAuthType = {
  Anonymous: "Anonymous",
  Guest: "Guest",
  Google: "Google",
} as const;
export type EAuthType = (typeof EAuthType)[keyof typeof EAuthType];

export interface IAuthData {
  authType: EAuthType | null;
  authUser: User | null;
  authUsername: string;
}
export var defaultAuthData: IAuthData = {
  authType: null as EAuthType | null,
  authUser: null as User | null,
  authUsername: "" as string,
};

export const AuthChannel = new EventRadio<IAuthData>("auth");
