import {
  SELECT_ONE,
  DESELECT_ONE,
  SELECT_ALL,
  DESELECT_ALL
} from '../constants/Selected'

const initialState = {
  selected:[]
}

export default function selected(state = initialState, action) {

  switch (action.type) {
    case DESELECT_ONE:
      if (state.selected.indexOf(action.payload)>-1) state.selected.splice(state.selected.indexOf(action.payload), 1)
      return { ...state, selected: state.selected }

    case SELECT_ONE:
      state.selected.push(action.payload)
      return { ...state, selected: state.selected }

    case DESELECT_ALL:
      return { ...state, selected: [] }

    case SELECT_ALL:
      return { ...state, selected: action.payload}

    default:
      return state;
  }

}
