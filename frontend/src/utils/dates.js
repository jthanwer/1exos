import moment from 'moment'

function dateFormatter(timestamp) {
  moment.locale('fr');
  let date = new Date(timestamp)
  let formattedTime = moment(date).format('LL')
  return formattedTime
}

export { dateFormatter }