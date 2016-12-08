import { combineReducers } from 'redux'
import friends from './friends'
import selected  from './selected'

export default combineReducers({
  friends,
  selected
})
