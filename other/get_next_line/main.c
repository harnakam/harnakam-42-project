#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include "get_next_line.h"

static int	g_fail = 0;

static void	check(const char *name, int ok)
{
	printf("[%s] %s\n", ok ? "OK" : "KO", name);
	if (!ok)
		g_fail++;
}

/* 内容を一時ファイルに書き、get_next_line で全行読んで expected 配列と比較 */
static void	run_case(const char *name, const char *content,
		const char **expected, int n)
{
	char	path[] = "/tmp/gnl_test_XXXXXX";
	int		fd;
	int		i;
	int		ok;
	char	*line;

	fd = mkstemp(path);
	write(fd, content, strlen(content));
	close(fd);
	fd = open(path, O_RDONLY);
	ok = 1;
	i = 0;
	while (i < n)
	{
		line = get_next_line(fd);
		if (!line || strcmp(line, expected[i]) != 0)
			ok = 0;
		free(line);
		i++;
	}
	line = get_next_line(fd);
	if (line != NULL)
		ok = 0;
	free(line);
	close(fd);
	unlink(path);
	check(name, ok);
}

static void	run_tests(void)
{
	const char	*e1[] = {"hello\n", "world\n"};
	const char	*e2[] = {"hello\n", "world"};
	const char	*e3[] = {"\n", "\n", "a\n"};
	const char	*e4[] = {"only"};
	char		*big;
	const char	*e5[1];
	int			fd;
	char		*line;

	printf("BUFFER_SIZE = %d\n", BUFFER_SIZE);
	run_case("two lines with trailing newline", "hello\nworld\n", e1, 2);
	run_case("no trailing newline", "hello\nworld", e2, 2);
	run_case("empty lines", "\n\na\n", e3, 3);
	run_case("single line without newline", "only", e4, 1);
	run_case("empty file", "", NULL, 0);
	big = malloc(10002);
	memset(big, 'x', 10000);
	big[10000] = '\n';
	big[10001] = '\0';
	e5[0] = big;
	run_case("long line (10000 chars)", big, e5, 1);
	free(big);
	check("invalid fd (-1)", get_next_line(-1) == NULL);
	fd = open("/tmp", O_RDONLY);
	line = get_next_line(fd);
	check("directory fd returns NULL", line == NULL);
	free(line);
	close(fd);
}

int	main(int argc, char **argv)
{
	int		fd;
	int		n;
	char	*line;

	if (argc < 2)
	{
		run_tests();
		printf("%s\n", g_fail ? "SOME TESTS FAILED" : "ALL TESTS PASSED");
		return (g_fail != 0);
	}
	fd = open(argv[1], O_RDONLY);
	if (fd < 0)
		return (perror(argv[1]), 1);
	n = 1;
	while ((line = get_next_line(fd)))
	{
		printf("%d: %s", n++, line);
		if (!strchr(line, '\n'))
			printf("\n");
		free(line);
	}
	close(fd);
	return (0);
}
