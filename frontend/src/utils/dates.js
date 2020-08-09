import moment from 'moment'

function dateFormatter(timestamp) {
  moment.locale('fr')
  let date = new Date(timestamp)
  let formattedTime = moment(date).format('L')
  return formattedTime
}

export { dateFormatter }
