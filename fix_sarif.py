# Adjust the function to also fix startColumn and endColumn issues in the SARIF file.

def fix_sarif_columns(sarif_path):
    import json
    
    with open(sarif_path, 'r') as file:
        sarif_data = json.load(file)
    
    # Applying fixes for the identified issues related to columns
    for run in sarif_data.get("runs", []):
        for result in run.get("results", []):
            for location in result.get("locations", []):
                physical_location = location.get("physicalLocation", {})
                region = physical_location.get("region", {})
                # Fix startLine and endLine if necessary
                if "startLine" in region and region["startLine"] < 1:
                    region["startLine"] = 1
                if "endLine" in region and region["endLine"] < 1:
                    region["endLine"] = 1
                # Fix startColumn and endColumn
                if "startColumn" in region and region["startColumn"] < 1:
                    region["startColumn"] = 1
                if "endColumn" in region and region["endColumn"] < 1:
                    region["endColumn"] = 1
    
    # Write the fixed SARIF data back to a new file
    corrected_file_path = sarif_path.replace(".sarif", "fixed_semgrep.sarif")
    with open(corrected_file_path, 'w') as file:
        json.dump(sarif_data, file, indent=4)
    
    return corrected_file_path

corrected_sarif_file_path = fix_sarif_columns('semgrep.sarif')
corrected_sarif_file_path