import config
import json


class HealthAPIDataManager:

    @staticmethod
    def _get_indicators_data():
        response_text = HealthAPIDataManager._fetch_text_from_url(config.HEALTH_INDICATORS_URL)
        try:
            indicators_data = json.loads(response_text)['value']
        except (TypeError, ConnectionError, Exception) as e:
            config.logger.critical(e, exc_info=True)
            config.exit_program()
        return indicators_data

    @staticmethod
    def get_data():
        indicators_data = HealthAPIDataManager._get_indicators_data()
        for health_indicator in config.HealthIndicator:
            url = config.HEALTH_INDICATOR_URL.replace(config.HEALTH_INDICATOR, health_indicator.value)
            response_text = HealthAPIDataManager._fetch_text_from_url(url)
            try:
                countries = json.loads(response_text)['value']
            except (TypeError, ConnectionError, Exception) as e:
                config.logger.critical(e, exc_info=True)
                config.exit_program()
            for indicator_data in indicators_data:
                if indicator_data['IndicatorCode'] == health_indicator.value:
                    indicator_description = indicator_data['IndicatorName']
                    break
            config.countries_health_data[health_indicator.name] = (indicator_description, countries)

    @staticmethod
    def _fetch_text_from_url(URL):
        config.logger.info(f'Started fetching data from {URL}')
        try:
            response = config.requests.get(URL)
        except (TypeError, ConnectionError, Exception) as e:
            config.logger.critical(e, exc_info=True)
            config.exit_program()
        if response.status_code != config.HTTP_SUCCESS:
            config.logger.critical(f'Error fetching data from {URL}')
            config.exit_program()
        config.logger.info(f'Finished fetching data from {URL}')
        return response.text
