import api from "@/services/api";

export default {
  get_pie_chart_data(sector, year) {
    return api.get(`summary/user/${sector}/${year}/`)
      .then(response => response.data);
  },
  get_bar_chart_data(sector) {
    return api.get(`summary/user/${sector}/stackbars/`)
      .then(response => response.data);
  },
  get_ts_data(sector) {
    return api.get(`summary/user/${sector}/ts/`)
      .then(response => response.data);
  },
};