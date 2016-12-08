import {
  SET_FRIENDS,
  CLEAR_FRIENDS
} from '../constants/Friends'

const initialState = {
  friends:[]
}

export default function filter(state = initialState, action) {

  switch (action.type) {
    case SET_FRIENDS:
      return { ...state, friends: action.payload}

    case CLEAR_FRIENDS:
      return {...state, friends: []}
    default:
      return state;

}
}
