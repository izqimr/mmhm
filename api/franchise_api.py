import re

from common.request import Request
from common.yml import Yml


class FranchiseApi:
    PLACEHOLDER = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def __init__(self):
        self.yml = Yml()
        self.headers = self.yml.get_headers()

    def intention_apply(self, json, headers=None):
        url = "gateway/store-franchise-service/intention/manage/resubmit/apply"
        use_headers = headers or self.headers
        return Request().post(url, json=json, headers=use_headers)

    def upload_contract(self, json, headers=None):
        url = "gateway/store-franchise-service/contract/upload"
        use_headers = headers or self.headers
        return Request().post(url, json=json, headers=use_headers)

    def run_flow(self, flow_data, extra_context=None, start_index=0, end_index=None):
        context = dict(flow_data.get("context", {}))
        if extra_context:
            context.update(extra_context)

        steps = flow_data.get("steps", [])
        if end_index is None:
            selected_steps = steps[start_index:]
        else:
            selected_steps = steps[start_index:end_index]

        results = []
        for step in selected_steps:
            if not step.get("enabled", True):
                continue

            body = self._replace_vars(step.get("body", {}), context)
            headers = self._replace_vars(step.get("headers", self.headers), context)
            response = Request().send(
                method=step.get("method", "POST"),
                url=step["url"],
                json=body,
                headers=headers,
            )
            response_json = response.json()

            for key, path in step.get("extract", {}).items():
                context[key] = self._get_value_by_path(response_json, path)

            results.append({"step": step.get("name", "unnamed_step"), "response": response_json})

        return {"context": context, "results": results}

    def _replace_vars(self, value, context):
        if isinstance(value, dict):
            return {k: self._replace_vars(v, context) for k, v in value.items()}
        if isinstance(value, list):
            return [self._replace_vars(v, context) for v in value]
        if not isinstance(value, str):
            return value

        full = self.PLACEHOLDER.fullmatch(value)
        if full:
            return context.get(full.group(1), value)

        return self.PLACEHOLDER.sub(lambda m: str(context.get(m.group(1), m.group(0))), value)

    def _get_value_by_path(self, data, path):
        current = data
        for segment in path.split("."):
            if not isinstance(current, dict):
                return None
            current = current.get(segment)
        return current
