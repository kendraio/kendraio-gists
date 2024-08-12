import json
import requests
import collections

INPUT_FILE_URL = 'https://app.kendra.io/flows'
LAUNCH_BLOCK_TYPE = 'launch'

# Read JSON data from the URL
response = requests.get(INPUT_FILE_URL)
flows_data = response.json()

flow_launch_info = collections.defaultdict(list)

def collect_launch_block_info(blocks, flow_id, adapter_name, workflow_id, action_titles):
    """Collect statistics for all launch blocks in the blocks."""
    count = 0
    urls = []
    titles = []
    for block in blocks:
        if isinstance(block, dict):
            if block.get('type') == LAUNCH_BLOCK_TYPE:
                adapter_name = block.get('adapter', adapter_name)
                workflow_id = block.get('workflowId', workflow_id)
                url = f"https://app.kendra.io/{adapter_name}/{workflow_id}"
                if url not in urls:
                    urls.append(url)
                count += 1
                if action_titles:
                    titles.append(action_titles[-1])
            for key, value in block.items():
                if isinstance(value, list):
                    sub_count, sub_urls, sub_titles = collect_launch_block_info(value, flow_id, adapter_name, workflow_id, action_titles)
                    count += sub_count
                    urls.extend([url for url in sub_urls if url not in urls])
                    titles.extend(sub_titles)
                elif isinstance(value, dict):
                    sub_count, sub_urls, sub_titles = collect_launch_block_info([value], flow_id, adapter_name, workflow_id, action_titles)
                    count += sub_count
                    urls.extend([url for url in sub_urls if url not in urls])
                    titles.extend(sub_titles)
        elif isinstance(block, list):
            sub_count, sub_urls, sub_titles = collect_launch_block_info(block, flow_id, adapter_name, workflow_id, action_titles)
            count += sub_count
            urls.extend([url for url in sub_urls if url not in urls])
            titles.extend(sub_titles)
        elif block == 'buttons':
            for button in value:
                action_titles.append(button.get('label', ''))
    return count, urls, titles

def process_flows(flows):
    """Process each flow and collect launch block info."""
    for flow in flows:
        flow_id = flow.get('id', 'unknown')
        adapter_name = flow.get('adapterName', 'unknown')
        workflow_id = flow.get('workflowId', 'unknown')
        title = flow.get('title', '')
        if 'blocks' in flow:
            count, urls, titles = collect_launch_block_info(flow['blocks'], flow_id, adapter_name, workflow_id, [])
            for url in urls:
                flow_launch_info[adapter_name].append((url, count, title, flow_id, titles))

# Process the flows
process_flows(flows_data)

# Calculate total counts per adapter
adapter_totals = {adapter_name: sum(count for _, count, _, _, _ in blocks)
                  for adapter_name, blocks in flow_launch_info.items()}

# Sort and print the grouped data with total counts
for adapter_name, blocks in sorted(flow_launch_info.items(), key=lambda x: -adapter_totals[x[0]]):
    total_count = adapter_totals[adapter_name]
    print(f"\nAdapter: {adapter_name} (Total: {total_count})")
    sorted_blocks = sorted(blocks, key=lambda x: -x[1])
    for url, count, title, flow_id, titles in sorted_blocks:
        print(f"{url} ({count})")
        if titles:
            for t in titles:
                print(f"  - Title: {t}")
