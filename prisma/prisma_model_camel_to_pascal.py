"""
Case conversion script for schema.prisma

Script is used to change casing for all prisma models in schema.prisma
This is to ensure right casing for python classes which prisma generates
"""

with open("schema.prisma", "r", encoding="utf-8") as file:
  lines = file.readlines()
  added_lines = 0
  for i, line in enumerate(lines.copy()):
    line_list = line.split()
    try:
      if line_list[0] == "model":
        to_map = line_list[1]
        line_list[1] = to_map.replace("_", " ").title().replace(" ", "")
        lines[i + added_lines] = " ".join(line_list) + "\n"

        for j, tmp_line in enumerate(lines.copy()):
          tmp_line_list = tmp_line.split()
          try:
            if tmp_line_list[1] in [to_map, to_map + "[]", to_map + "?"]:
              if tmp_line_list[1].endswith("[]"):
                tmp_line_list[1] = to_map.replace("_", " ").title().replace(
                    " ", "") + "[]"
                lines[j] = "  " + " ".join(tmp_line_list) + "\n"

              elif tmp_line_list[2].startswith("@relation"):
                tmp_line_list[1] = to_map.replace("_",
                                                  " ").title().replace(" ", "")
                lines[j] = "  " + " ".join(tmp_line_list) + "\n"
          except IndexError:
            pass

        lines.insert(i + 1 + added_lines, f"  @@map(\"{to_map}\")\n")
        added_lines += 1
      elif line_list[0] == "enum":
        to_map = line_list[1]
        line_list[1] = to_map.replace("_", " ").title().replace(" ", "")
        lines[i + added_lines] = " ".join(line_list) + "\n"
        for j, tmp_line in enumerate(lines.copy()):
          tmp_line_list = tmp_line.split()
          try:
            if tmp_line_list[1] in [to_map, to_map + "?"]:
              if tmp_line_list[1].endswith("?"):
                tmp_line_list[1] = to_map.replace("_", " ").title().replace(
                    " ", "") + "?"
                lines[j] = "  " + " ".join(tmp_line_list) + "\n"
              else:
                tmp_line_list[1] = to_map.replace("_",
                                                  " ").title().replace(" ", "")
                lines[j] = "  " + " ".join(tmp_line_list) + "\n"
          except IndexError:
            pass
    except IndexError:
      pass

with open("schema.prisma", "w", encoding="utf-8") as file:
  file.writelines(lines)
