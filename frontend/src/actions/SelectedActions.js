import {
  SELECT_ONE,
  DESELECT_ONE,
  SELECT_ALL,
  DESELECT_ALL
} from '../constants/Selected'


export function selectFriend(friend) {
  return {
      type: SELECT_ONE,
      payload: friend
    }
}

export function selectAll(friendlist) {
  return {
      type: SELECT_ALL,
      payload: friendlist
    }
}

export function deselectAll() {
  return {
      type: DESELECT_ALL,
    }
}

export function deselectFriend(friend) {
  return {
      type: DESELECT_ONE,
      payload: friend
    }
}
