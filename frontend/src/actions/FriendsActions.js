import {
  SET_FRIENDS,
  CLEAR_FRIENDS
} from '../constants/Friends'


export function setFriends(friendlist) {
  return {
      type: SET_FRIENDS,
      payload: friendlist
    }
}

export function clearFriends() {
  return {
      type: CLEAR_FRIENDS
    }
}
