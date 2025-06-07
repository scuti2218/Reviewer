import { signInWithPopup, signOut } from 'firebase/auth'
import { auth, provider } from '@services/firebase'

export const login = () => signInWithPopup(auth, provider)
export const logout = () => signOut(auth)
export const currentUser = () => auth.currentUser